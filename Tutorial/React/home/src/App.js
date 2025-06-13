import logo from './logo.svg';
import './App.css';

const multbutton = () => {
  var output =[];
  for (let i = 1; i <= 10; i++) {
    output.push(<button key={i} className="mult-button">{i}</button>);
  }
  return output;
};

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <h1 style={{fontSize: '100px',color:'red'}}>Welcome to React!</h1>
        <h1 className='App-title'>Welcome to React!</h1>
        <div className="mult-buttons">
          {multbutton()}
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
