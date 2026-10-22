import allure
import pytest
from playwright.sync_api import expect

@allure.epic('Тестрование UI')
@allure.feature('Отзывы')
@pytest.mark.ui
class TestMovieReview:

    @allure.title('Оставление отзыва под фильмом')
    def test_movie_review(self, logged_in_page, movie_page, create_movie, page):
        expect(page.locator('[data-qa-id="profile_page_button"]')).to_be_visible()
        
        movie_id = create_movie['id']
        movie_page.open(movie_id)
        review_text = f'Фильм очень понравился! Заставил задуматься.'
        movie_page.leave_review(review_text)
        expect(page.get_by_text(review_text)).to_be_visible(timeout=10000)