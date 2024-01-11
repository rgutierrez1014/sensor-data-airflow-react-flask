import { useState } from 'react';
import axios from 'axios';
import moment from 'moment';


function App() {
  const [data, setData] = useState(null);
  const [flashMessage, setFlashMessage] = useState('');
  const [flashClass, setFlashClass] = useState('flash-message');

  const clearFlash = () => {
    setFlashMessage('');
    setFlashClass('flash-message');
  }
  const setFlash = (msg) => {
    setFlashMessage(msg);
    setFlashClass('flash-message has-message');
    setTimeout(() => {
      clearFlash();
    }, 5000);
  }

  const handleRefreshData = (e) => {
    clearFlash();
    axios
      .get('http://localhost:8000/get-current-data')
      .then((res) => {
        let data = res.data.data;
        setData(data);
        setFlash('Current data retrieved successfully!');
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
      });
  }
  const handleTriggerDAG = (e) => {
    clearFlash();
    axios
      .get('http://localhost:8000/trigger')
      .then((res) => {
        console.log('DAG trigger successful!');
        setFlash('DAG trigger successful!');
      })
      .catch((error) => {
        if (error.response) {
          console.log("Error: ", error.response.data.message);
        } else if (error.request) {
          console.log("Error: ", error.request);
        } else {
          console.log("Error: ", error.message);
        }
        setFlash('An error occurred while trying to trigger the DAG! Please try again.');
      });
  }
  
  return (
    <div className="container">
      <p className={flashClass}>{flashMessage}</p>
      <h1>Sample Sensor Data "Dashboard" - Robert Gutierrez</h1>
      <br />
      <button onClick={() => handleTriggerDAG()}>Trigger DAG</button>&nbsp;&nbsp;
      <button onClick={() => handleRefreshData()}>Refresh Data</button>
      <br />
      <h4>Current Data</h4>
      <div>{!data ? (<p>No data yet. Click "Refresh Data" above to see if the data has been processed by Airflow.</p>) : (
        <>
          <small>Terminology: UFP = Ultrafine Particles, BC = Black Carbon, NO2 = Nitrogen Dioxide</small>
          <table>
            <thead>
              <tr>
                <th>Calculated at</th>
                <th>UFP Mean</th>
                <th>UFP Median</th>
                <th>UFP Standard Deviation</th>
                <th>BC Mean</th>
                <th>BC Median</th>
                <th>BC Standard Deviation</th>
                <th>NO2 Mean</th>
                <th>NO2 Median</th>
                <th>NO2 Standard Deviation</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => {
                return (
                  <tr key={row.id}>
                    <td>{moment(row.created_at).format('MM/DD/YYYY hh:mm:ss A [UTC]')}</td>
                    <td>{parseFloat(row.ufp_mean).toFixed(2)}</td>
                    <td>{parseFloat(row.ufp_median).toFixed(2)}</td>
                    <td>{parseFloat(row.ufp_stddev).toFixed(2)}</td>
                    <td>{parseFloat(row.bc_mean).toFixed(2)}</td>
                    <td>{parseFloat(row.bc_median).toFixed(2)}</td>
                    <td>{parseFloat(row.bc_stddev).toFixed(2)}</td>
                    <td>{parseFloat(row.no2_mean).toFixed(2)}</td>
                    <td>{parseFloat(row.no2_median).toFixed(2)}</td>
                    <td>{parseFloat(row.no2_stddev).toFixed(2)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      )}</div>
    </div>
  );
}

export default App;
