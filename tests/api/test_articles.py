import pytest
import uuid
import requests
from api.articles_api import CannotRetrieveArticleException
from api.articles_api import ArticleAlreadyExistsException
from api.auth_api import AuthService

def test_get_articles_all(articles_service):
    response = articles_service.get_articles()
    assert response.status_code == 200, f"Failed: {response.status_code} {response.text}"
    ret = response.json()
    assert isinstance(ret['articles'], list)
    assert ret['articlesCount'] >= len(ret['articles'])

def test_get_articles_with_limit(articles_service):
    response = articles_service.get_articles(limit=1)
    assert response.status_code == 200, f"Failed: {response.status_code} {response.text}"
    ret = response.json()
    assert ret['articlesCount'] >= len(ret['articles'])
    assert len(ret['articles']) == 1

def test_create_article(articles_service, auth_service):
    response = articles_service.create_article(
        title='Clockwork Orange',
        description='Lorem Ipsum',
        body='Lorem Ipsum',
        tagList=['tag']
    )
    assert response.status_code == 201, f"Failed: {response.status_code} {response.text}"
    ret = response.json()
    assert ret['article']['title'] == 'Clockwork Orange'
    assert ret['article']['description'] == 'Lorem Ipsum'
    assert ret['article']['body'] == 'Lorem Ipsum'

def test_create_duplicate_article(articles_service, mocker):
    payload = dict(
        title=f'Clockwork Orange {uuid.uuid4()}',
        description='Lorem Ipsum',
        body='Lorem Ipsum',
        tagList=['tag'],
    )

    first = articles_service.create_article(**payload)
    assert first.status_code in (200, 201)

    # Second call is mocked because data does not persist; Articles will not duplicate
    mock_response = requests.Response()
    mock_response.status_code = 409

    mocker.patch.object(
        articles_service.client,
        "post",
        return_value=mock_response
    )

    with pytest.raises(ArticleAlreadyExistsException) as exc_info:
        articles_service.create_article(**payload)

    assert isinstance(exc_info.value, ArticleAlreadyExistsException)

def test_delete_article(articles_service, mocker):
    # 1. Create a fake HTTP response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    # 2. Replace the actual HTTP DELETE method
    mocker.patch.object(
        articles_service.client,
        "delete",
        return_value=mock_response,
    )

    # 3. Call the service method
    slug = "test-article"
    response = articles_service.delete_article(slug)

    # 4. Verify the DELETE request
    articles_service.client.delete.assert_called_once_with(
        f"/articles/{slug}"
    )

    # 5. Verify the response was checked
    mock_response.raise_for_status.assert_called_once()

    # 6. Verify the returned response
    assert response == mock_response

def test_update_article(articles_service, auth_service):
    #1. Create an article and capture its slug
    response = articles_service.create_article(
        title='Clockwork Orange',
        description='Lorem Ipsum',
        body='Lorem Ipsum',
        tagList=['tag']
    )
    assert response.status_code == 201, f"Failed: {response.status_code} {response.text}"
    slug = response.json()['article']['slug']

    #2. Update it
    response = articles_service.update_article(
        slug,
        title="Clockwork Orange",
        description="Updated description",
        body="Updated body"
    )

    assert response.status_code == 200, f"Failed: {response.status_code} {response.text}"
    ret = response.json()
    assert ret['article']['title'] == 'Clockwork Orange'
    assert ret['article']['description'] == 'Updated description'
    assert ret['article']['body'] == 'Updated body'

# def test_update_article(articles_service, mocker):
#     # 1. Create a fake HTTP response
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.raise_for_status.return_value = None
#
#     # 2. Replace the actual HTTP DELETE method
#     mocker.patch.object(
#         articles_service.client,
#         "put",
#         return_value=mock_response,
#     )
#
#     # 3. Call the service method
#     slug = "test-article"
#     response = articles_service.update_article(slug)
#
#     # 4. Verify the PUT request
#     articles_service.client.put.assert_called_once_with(
#         f"/articles/{slug}"
#     )
#
#     # 5. Verify the response was checked
#     mock_response.raise_for_status.assert_called_once()
#
#     # 6. Verify the returned response
#     assert response == mock_response
#
