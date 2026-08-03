const API_URL = "http://localhost:8000";

export async function getEvents(){
    const response=await fetch(`${API_URL}/events`);
    const data=await response.json();
    return data;
}