import { useState } from 'react';
import axios from 'axios';


function App() {
  const [dataDescription, setDataDescription] = useState('No data yet. Data will be available once it has been processed by Airflow.');

  const handleUpload = (e) => {
    setDataDescription('Loading...');
    axios
      .get('http://localhost:8000/get-current-data')
      .then((res) => {
        console.log('Axios GET request successful!')
        // do something with data
        let desc = "Data";
        setDataDescription(desc);
      })
      .catch((error) => {
        if (error.response) {
          console.log("Error: ", error.response.data.message);
        } else if (error.request) {
          console.log("Error: ", error.request);
        } else {
          console.log("Error: ", error.message);
        }
        setDataDescription('An error occurred; unable to process! Please try again.')
      });
  }
  
  return (
    <div className="container">
      <h1>Sample Sensor Data "Dashboard" - Robert Gutierrez</h1>
      <br />
      <h4>Current Data</h4>
      <p>No data yet.</p>
    </div>
  );
}

export default App;
