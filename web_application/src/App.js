import './App.css';
import {useState} from "react";
import Spinner from 'react-bootstrap/Spinner';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


function GetComics(setComicsUrl, setLoading, setDataForRegenerate) {
    const comics_topic = document.getElementById("formComicsTopic").value
    const image_style = document.getElementById("formImageStyle").value || "cyberpunk"
    const width_images = document.getElementById("formWidthImages").value || "2"
    const height_images = document.getElementById("formHeightImages").value || "3"
    setComicsUrl("http://127.0.0.1:5000/generate_comics/?" + new URLSearchParams({comics_topic, image_style, width_images, height_images}))
    setDataForRegenerate({comics_topic, image_style, width_images, height_images})
    setLoading(true)
}

function OnImageLoaded(setLoading) {
    setLoading(false)
}

function ClearSituation(setComicsUrl, setLoading) {
    setComicsUrl("")
    setLoading(false)
}

function RegenerateComics(dataForRegenerate, setComicsUrl, setLoading) {
    setComicsUrl("http://18.185.249.159:5000/generate_comics/?" + new URLSearchParams({regenerated: Math.floor(Math.random() * 100000), ...dataForRegenerate}))
    setLoading(true)
}

function App() {
    const [comicsURL, setComicsUrl] = useState("")
    const [loading, setLoading] = useState(false)
    const [dataForRegenerate, setDataForRegenerate] = useState([])

    console.log("App")
    console.log(comicsURL)

    return (<div className="App">
        {comicsURL === "" && loading === false &&
            <div style={{display: "flex", flexDirection: "row", justifyContent: "left", textAlign: "left", minWidth: "50%"}}>
                <Form style={{width: "100%"}}>
                    <Form.Group className="mb-3" controlId="formComicsTopic">
                        <Form.Label><h5>Comics topic</h5></Form.Label>
                        <Form.Control as="textarea" rows={3} placeholder="Create a comics about..."/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formImageStyle">
                        <Form.Label><h5>Image style</h5></Form.Label>
                        <Form.Control type="textarea" placeholder="cyberpunk"/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formWidthImages">
                        <Form.Label><h5>Number of images in width</h5></Form.Label>
                        <Form.Control type="number" placeholder="2"/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formHeightImages">
                        <Form.Label><h5>Number of images in height</h5></Form.Label>
                        <Form.Control type="number" placeholder="3"/>
                    </Form.Group>

                    <Button variant="primary" type="submit" onClick={() => GetComics(setComicsUrl, setLoading, setDataForRegenerate)}>Generate</Button>
                </Form>
            </div>
        }
        {loading === true && <Spinner animation="border" role="status" variant="primary"/>}
        {comicsURL !== "" &&
            <div style={{display: "flex", flexDirection: "column"}}>
                <img style={loading ? {"display": "none"} : {}} src={comicsURL} alt="comics"
                     onLoad={() => {
                         OnImageLoaded(setLoading)
                     }}
                     onChange={() => {
                         OnImageLoaded(setLoading)
                     }}
                />
                {loading === false &&
                    <div style={{display: "flex", flexDirection: "row", width: "100%"}}>
                        <Button variant="primary" type="submit" onClick={() => ClearSituation(setComicsUrl, setLoading)}>Clear</Button>
                        <Button variant="primary" type="submit"
                                onClick={() => RegenerateComics(dataForRegenerate, setComicsUrl, setLoading)}>Regenerate</Button>
                    </div>
                }
            </div>
        }
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
