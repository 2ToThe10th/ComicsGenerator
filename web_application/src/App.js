import logo from './logo.svg';
import './App.css';
import {useState} from "react";

async function GetComics(setComics) {
    let comics_topic = document.getElementById("comics").value
    console.log(comics_topic)
    const comics_data = await (await fetch("http://127.0.0.1:5000/get_comics/?" + new URLSearchParams({comics_topic}))).json()
    console.log(`Get comics data: ${comics_data}`)
    setComics(comics_data)
}

function App() {
    const [comics, setComics] = useState([])

    console.log("App")
    console.log(comics)

    return (<div className="App">
        <header className="App-header">
            {comics.length === 0 &&
                <input type="text" id="comics" name="comics"/>
            }
            {comics.length === 0 &&
                <input type="Submit" name="Get Comics" onClick={() => GetComics(setComics)}/>
            }
            {comics.length === 6 && <Comics comics={comics}/>}
            {comics.length !== 0 && comics.length !== 6 && <h1>Incorrect panels length</h1>}
        </header>
    </div>);
}

function Comics(props) {
    const comics = props.comics
    const panels = comics.map((x, _) => <Panel panel={x.panel} phrase={x.phrase}/>)
    return <div style={{display: "flex", flexDirection: "column"}}>
        {[...Array(3)].map((_, i) => <div
            style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>{panels[2 * i]}{panels[2 * i + 1]}</div>)}
    </div>
}

function Panel(props) {
    const panel = props.panel
    const phrase = props.phrase

    return (
        <img src={`http://127.0.0.1:5000/get_panel/?` + new URLSearchParams({panel, phrase})} alt={phrase} height={128} width={128}/>
    )
}

export default App;
