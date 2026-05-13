import pytest


class TestGetActivities:
    def test_get_all_activities(self, client):
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Swimming Club", "Digital Art", "Theater Club", "Debate Team", "Robotics Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]
            assert isinstance(data[activity]["participants"], list)


class TestSignupForActivity:
    def test_signup_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "test@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"

        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_invalid_activity(self, client):
        # Arrange
        invalid_activity = "Nonexistent Activity"
        email = "test@example.com"

        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_already_signed_up(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"


class TestUnregisterParticipant:
    def test_unregister_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Removed {email} from {activity_name}"

        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_invalid_activity(self, client):
        # Arrange
        invalid_activity = "Nonexistent Activity"
        email = "test@example.com"

        # Act
        response = client.delete(f"/activities/{invalid_activity}/participants?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_participant_not_found(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notsignedup@example.com"  # Not in participants

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Participant not found in activity"