import './App.css';
import {useState} from "react";

async function GetComics(setComicsUrl) {
    const comics_topic = document.getElementById("comics").value
    const image_style = "cyberpunk"
    const width_images = 2
    const height_images = 3
    setComicsUrl("http://127.0.0.1:5000/generate_comics/?" + new URLSearchParams({comics_topic, image_style, width_images, height_images}))
}

function App() {
    const [comicsUrl, setComicsUrl] = useState("")

    console.log("App")
    console.log(comicsUrl)

    return (<div className="App">
        <header className="App-header">
            {comicsUrl === "" &&
                <input type="text" id="comics" name="comics"/>
            }
            {comicsUrl === "" &&
                <input type="Submit" name="Get Comics" onClick={() => GetComics(setComicsUrl)}/>
            }
            {comicsUrl !== "" && <img src={comicsUrl} alt="comics"/>}
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
