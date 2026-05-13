class TestRoot:
    def test_root_redirect(self, client):
        # Arrange
        expected_url = "/static/index.html"

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200  # RedirectResponse, but TestClient follows redirects by default?
        # Actually, RedirectResponse returns 307, but TestClient might follow it.
        # Let me check: FastAPI RedirectResponse is 307, but TestClient follows redirects unless follow_redirects=False

        # Since it's a redirect, and TestClient follows by default, it should get the static file.
        # But to test the redirect, perhaps use follow_redirects=False

        # Arrange
        # Act with no follow
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == expected_url