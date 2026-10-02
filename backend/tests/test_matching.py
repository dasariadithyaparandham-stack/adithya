import unittest

from app.services.skill_matcher import analyze_resume_against_job
from app.services.auth import create_access_token, decode_access_token, hash_password, verify_password
from app.services.recommender import build_recommendations


class MatchingTests(unittest.TestCase):
    def test_weighted_score_and_priority_use_job_importance(self):
        result = analyze_resume_against_job(
            ['Python', 'SQL'],
            1,
            {
                'skills': {'Python': 10, 'Statistics': 8, 'Excel': 3},
                'categories': {'Python': 'Programming', 'Statistics': 'Analytics', 'Excel': 'Data'},
            },
        )
        self.assertEqual(result['matched_skills'], ['Python', 'SQL'][:1])
        self.assertEqual(result['priority_summary']['High'], ['Statistics'])
        self.assertEqual(result['priority_summary']['Low'], ['Excel'])
        self.assertGreater(result['weighted_score'], 0)

    def test_detected_skills_are_not_reported_as_unrelated_matches(self):
        result = analyze_resume_against_job(
            ['Python', 'Docker'],
            1,
            {'skills': {'Python': 10}, 'categories': {'Python': 'Programming'}},
        )
        self.assertEqual(result['matched_skills'], ['Python'])
        self.assertEqual(result['detected_skills'], ['Docker', 'Python'])

    def test_learning_recommendations_change_with_experience_level(self):
        fresher = build_recommendations(['Python'], 'fresher')[0]
        experienced = build_recommendations(['Python'], 'experienced')[0]
        self.assertIn('fundamentals', fresher['experience_guidance'])
        self.assertIn('architecture', experienced['experience_guidance'])
        self.assertTrue(fresher['learning_resources'][0]['url'].startswith('https://'))

    def test_learning_recommendations_include_time_and_platform_details(self):
        recommendation = build_recommendations(['Python'], 'fresher')[0]
        self.assertIn('hour', recommendation['time_to_learn'].lower())
        self.assertIn('platform', recommendation['learning_resources'][0])
        self.assertTrue(recommendation['learning_resources'][0]['url'].startswith('https://'))

    def test_password_hash_and_signed_token_validation(self):
        password_hash = hash_password('correct-horse-battery')
        self.assertTrue(verify_password('correct-horse-battery', password_hash))
        self.assertFalse(verify_password('incorrect-password', password_hash))

        token = create_access_token(42)
        self.assertEqual(decode_access_token(token), 42)
        self.assertIsNone(decode_access_token(f'{token}tampered'))


if __name__ == '__main__':
    unittest.main()
