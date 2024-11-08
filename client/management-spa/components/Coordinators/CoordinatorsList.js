import React, { useEffect, useState } from "react";
import { fetchData, fetchEvents } from "../api";

const EventsList = () => {
    // useState: React hook that initializes the state variable events as an empty array
    // setEvents: function that allows updating of events whenever new data available
    const [events, setEvents] = useState([]);

    // useEffect: hook that runs side effects in React such as data fetching
    useEffect(() => {
        // retrieve event data from the API
        fetchEvents()
            // promise handler
            .then((response) => {
                setEvents(response.data);
            })
            .catch((error) => {
                console.error("Error fetching events:", error);
            });
    // empty array as the second argument means this effect will only run once, after the component mounts
    }, []);
}