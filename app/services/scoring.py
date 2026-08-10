#Windspeed : under 12 knots
#Wave Height: under a foot
#Precipitation: under 20%
from unittest import case
from app.services.cache import ttl_cache
from app import config, models
from app.services import timeline

#score a timeline of merged data records, returning a list of ConditionScore objects
def score_timeline(merged_list):
    scores = []

    for record in merged_list:
        score = 100  # Start with a perfect score

        # Windspeed scoring
        wind_penalty = min(40, max(0, (record.wind_speed_kn - 6) * 5))
        score -= wind_penalty

        # Wave height scoring
        if record.wave_height_m is not None:
            wave_penalty = min(30, max(0, (record.wave_height_m - 0.1) * 150))
            score -= wave_penalty

        # Precipitation scoring
        precip_penalty = min(20, max(0, (record.precipitation_probability - 10) * 0.5))
        score -= precip_penalty

        score= max(0, min(100, score))  # Ensure score is between 0 and 100

        #
        match score:
            case score if score >= 90:
                txt_rating = "Excellent"
            case score if score >= 70:
                txt_rating = "Good"
            case score if score >= 50:
                txt_rating = "Fair"
            case _:
                txt_rating = "Poor"

        scores.append(models.ConditionScore(date_time=record.date_time, score=round(score), txt_rating=txt_rating))

    return scores


#caching the score_location function for 30 minutes to avoid repeated calculations for the same location
@ttl_cache(1800)           
def score_location(lat, lon):
    return score_timeline(timeline.build_timeline(lat, lon))

if __name__ == "__main__":
    merged_list = timeline.build_timeline(*config.BALLAST_POINT)
    scores = score_timeline(merged_list)
    for score in scores:
        print(f"{score.date_time}: Score: {score.score}, Rating: {score.txt_rating}")