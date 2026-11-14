from api.client import ApiClient
import requests

class ArticlesException(Exception):
    """Base class for all ArticlesException exception"""

class CannotRetrieveArticleException(ArticlesException):
    """Unable to retrieve article(s) exception"""
    pass

class UnauthorizedActionArticleException(ArticlesException):
    """Unable to create article exception"""
    pass

class ArticleAlreadyExistsException(ArticlesException):
    """Article already exists exception"""
    pass

class ArticleValidationException(ArticlesException):
    """Validation Error - content is unprocessable"""

class ArticleService:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_articles(self, **kwargs):
        response = self.client.get(
            'articles/',
            params=kwargs,
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                raise CannotRetrieveArticleException(
                    f"Error retrieving article(s)"
                )
            raise
        return response

    def create_article(self, title, description, body, tagList=None):
        article = {
            "title" : title,
            "description" : description,
            "body" : body,
        }
        if tagList is not None:
            article["tagList"] = tagList

        response = self.client.post(
            'articles/',
            json={"article":article},
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                raise UnauthorizedActionArticleException(
                    f"User must be logged in to create an article"
                )
            elif response.status_code == 409:
                raise ArticleAlreadyExistsException(
                    f"Article already exists!"
                )
            raise
        return response

    def update_article(self, slug, title=None, description=None, body=None, tagList=None):
        article = {
            "title": title,
            "description": description,
            "body": body,
        }
        if tagList is not None:
            article["tagList"] = tagList

        response = self.client.put(
            f"/articles/{slug}",
            json={"article": article},
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 401:
                raise UnauthorizedActionArticleException(
                    f"User must be logged in to create an article"
                ) from exc
            elif response.status_code == 422:
                raise ArticleValidationException(
                    f"Unable to process and update the article"
                ) from exc
        return response

    def delete_article(self, slug: str):
        response = self.client.delete(
            f"/articles/{slug}"
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 401:
                raise UnauthorizedActionArticleException(
                    f"User must be logged in to create an article"
                ) from exc
            elif response.status_code == 422:
                raise ArticleValidationException(
                    f"Unable to process and update the article"
                ) from exc
        return response
