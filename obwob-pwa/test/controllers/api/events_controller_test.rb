require "test_helper"

class Api::EventsControllerTest < ActionDispatch::IntegrationTest
  test "should get current_question" do
    get api_events_current_question_url
    assert_response :success
  end

  test "should get submit_response" do
    get api_events_submit_response_url
    assert_response :success
  end
end
