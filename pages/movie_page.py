from pages.base_page import BasePage

class CinescopeMoviePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.review_submit_button = '[data-qa-id="movie_review_submit_button"]'

    def open(self, movie_id):
        self.open_url(f'{self.home_url}movies/{movie_id}')

    def leave_review(self, text: str):
        self.enter_text(self.review_input, text)
        self.click(self.review_submit_button)