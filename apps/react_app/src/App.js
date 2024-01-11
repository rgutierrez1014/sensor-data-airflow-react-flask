import { useState } from 'react';
import axios from 'axios';


function App() {
  const [dataDescription, setDataDescription] = useState('No data yet. Data will be available once it has been processed by Airflow.');
  const [flashMessage, setFlashMessage] = useState('');
  const [flashClass, setFlashClass] = useState('flash-message');

  const clearFlash = () => {
    setFlashMessage('');
    setFlashClass('flash-message');
  }
  const setFlash = (msg) => {
    setFlashMessage(msg);
    setFlashClass('flash-message has-message');
  }

  const handleRefreshData = (e) => {
    clearFlash();
    setDataDescription('Loading...');
    axios
      .get('http://localhost:8000/get-current-data')
      .then((res) => {
        // do something with data
        let data = res.data;
        setDataDescription(data);
      })
      .catch((error) => {
        if (error.response) {
          console.log("Error: ", error.response.data.message);
        } else if (error.request) {
          console.log("Error: ", error.request);
        } else {
          console.log("Error: ", error.message);
        }
        setFlash('An error occurred while refreshing data! Please try again.');
        setDataDescription('No data yet.');
      });
  }
  const handleTriggerDAG = (e) => {
    clearFlash();
    axios
      .get('http://localhost:8000/trigger')
      .then((res) => {
        console.log('DAG trigger successful!')
      })
      .catch((error) => {
        if (error.response) {
          console.log("Error: ", error.response.data.message);
        } else if (error.request) {
          console.log("Error: ", error.request);
        } else {
          console.log("Error: ", error.message);
        }
        setFlash('An error occurred while trying to trigger the DAG! Please try again.')
      });
  }
  
  return (
    <div className="container">
      <p class="flash-message">{flashMessage}</p>
      <h1>Sample Sensor Data "Dashboard" - Robert Gutierrez</h1>
      <br />
      <button onClick={() => handleTriggerDAG()}>Trigger DAG</button>
      <br />
      <h4>Current Data</h4>
      <div>{dataDescription}</div>
    </div>
  );
}

export default App;
