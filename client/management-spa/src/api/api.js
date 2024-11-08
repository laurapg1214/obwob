import axios from "axios";

const API_URL = "http://localhost:8000/api/";

// shared function to fetch data for all model endpoints below
const fetchData = (modelEndpoint) => {
    // get request to retrieve data from model endpoint of API
    return axios.get(`${API_URL}/${modelEndpoint}`)
        // promise handler that executes when axios.get request successful
        .then(response => {
            // access data from the response
            console.log(`${modelEndpoint} data:`, response.data);
            // return response data (array of objects) for use elsewhere
            return response.data;
        })
        // promise handler for errors (request fails)
        .catch(error => {
            // access data about the error
            console.error(`Error fetching ${modelEndpoint}:`, error);
            // lets calling function know error has occurred
            // for further handling e.g. showing error msg to user
            throw error;
        });
};

export const fetchCoordinators = () => fetchData('coordinators');

export const fetchDemographics = () => fetchData('demographics');

export const fetchEvents = () => fetchData('events');

export const fetchFacilitators = () => fetchData('facilitators');

export const fetchOrganizations = () => fetchData('organizations');

export const fetchParticipants = () => fetchData('participants');

export const fetchQuestions = () => fetchData('questions');

export const fetchReports = () => fetchData('reports');

export const fetchResponses = () => fetchData('responses');


