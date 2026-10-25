import pytest
from api.client import ApiClient

#build_url unit test
def test_build_url():
    c1 = ApiClient('https://api.realworld.show/api')
    c2 = ApiClient('https://api.realworld.show/api/')
    expected_url = 'https://api.realworld.show/api/articles'
    result_url_c1_1 = c1._build_url('articles')
    result_url_c1_2 = c1._build_url('/articles')
    result_url_c2_1 = c2._build_url('articles')
    result_url_c2_2 = c2._build_url('/articles')
    assert [result_url_c1_1,result_url_c1_2]  == [expected_url, expected_url]
    assert [result_url_c2_1, result_url_c2_2] == [expected_url, expected_url]

#GET
def test_get_wrapper(mocker):
    c = ApiClient('https://api.realworld.show/api')
    mock_get = mocker.patch("api.client.ApiClient._request")
    c.get( '/articles', timeout=10, params={'limit':5})
    mock_get.assert_called_once_with('GET',
                                     '/articles',
                                     timeout=10,
                                     params={'limit': 5}
                                     )
#POST
def test_post_wrapper(mocker):
    c = ApiClient('https://api.realworld.show/api')
    mock_get = mocker.patch("api.client.ApiClient._request")
    c.post( '/articles', timeout=10, params={'limit':5})
    mock_get.assert_called_once_with('POST',
                                     '/articles',
                                     timeout=10,
                                     params={'limit': 5}
                                     )

#DELETE
def test_delete_wrapper(mocker):
    c = ApiClient('https://api.realworld.show/api')
    mock_get = mocker.patch("api.client.ApiClient._request")
    c.delete( '/articles', timeout=10, params={'limit':5})
    mock_get.assert_called_once_with('DELETE',
                                     '/articles',
                                     timeout=10,
                                     params={'limit': 5}
                                     )

#UPDATE
def test_put_wrapper(mocker):
    c = ApiClient('https://api.realworld.show/api')
    mock_get = mocker.patch("api.client.ApiClient._request")
    c.put('/articles', timeout=10, params={'limit': 5})
    mock_get.assert_called_once_with('PUT',
                                     '/articles',
                                     timeout=10,
                                     params={'limit': 5}
                                     )
