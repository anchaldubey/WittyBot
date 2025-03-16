import Chatbot from "./Chatbot";
import "./index.css";


export default function App() {
 return (
   <div
     className="App"
     style={{
       height: "100vh",
       width: "100vw",
       display: "flex",
       flexDirection: "column",
       alignItems: "center",
       justifyContent: "center",
     }}
   >
     <div
       style={{
         textAlign: "center",
         fontSize: "24px",
         fontWeight: "bold",
         padding: "10px",
         width: "100%",
       }}
     >
       WittyBot
     </div>
     <div
       style={{
         width: "90%",
         height: "90%",
         display: "flex",
         flexDirection: "column",
         border: "3px solid black",
         borderRadius: "10px",
         overflowY: "auto",
       }}
     >
       <div
       style={{
         width: "90%",
         height: "90%",
         display: "flex",
         flexDirection: "column",
         overflowY: "auto",
         marginLeft: "80px",
         marginTop: "20px",
       }}
     >
       <Chatbot />
     </div>
     </div>
   </div>
 );
}
