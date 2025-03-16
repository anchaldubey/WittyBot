import { useState, useRef, useEffect } from "react";


const Chatbot = () => {
 const [input, setInput] = useState("");
 const [messages, setMessage] = useState([]);
 const messageEndRef = useRef(null);


 const scrollToBottom = () => {
   messageEndRef.current ?.scrollIntoView({behaviour: "smooth"})
 }


 useEffect(scrollToBottom, [messages])


 const handleSubmit = async (event) => {
   event.preventDefault();
   if(!input) return;
   setMessage((prevMessage) => [
     ...prevMessage,
     { user: "You", text: input, type: "user" },
   ]);
   setInput("");
   const query = input.replace(/\s+/g, "+");
   try {
     const response = await fetch(`http://127.0.0.1:5000/query/${query}`);
     const data = await response.json();
     const message = await data.top.res;
     console.log("response: ", response);
     console.log({ message });
     setMessage((prevMessages)=> [
       ...prevMessages,
       {user:"Chatbot", text:message, type:"bot"}
     ])
   } catch (err) {
     console.log("error ", err);
   } finally {
     isLoadingRef.current = false;
   }
 };


 return (
   <div style={{ height: "100%", width: "100%", display: "flex", flexDirection: "column", overflow: "hidden" }}>
     <div style={{flex: 1, overflowY: "auto"}}>
       {messages.map((message,index)=>(
           <div
           key={index}
           style={{
               display:"flex",
               justifyContent: message.type==="user" ? "flex-start" : "flex-end",
               margin: "5px",
           }}
           >
               <div
               style={{
                   background: message.type==="user" ? "#444654" : "#202123",
                   padding: "15px",
                   borderRadius: "10px",
                   maxWidth: "60%",
                   color: "white",
               }}
               >
                   <strong style={{marginRight: "10px"}}> {message.user} : </strong>
                   <span>{message.text}</span>
               </div>
           </div>
       ))}
       <div ref={messageEndRef}></div>
     </div>
     <form
 onSubmit={handleSubmit}
 style={{
   display: "flex",
   justifyContent: "center",
   position: "fixed",
   bottom: "20px",
   width: "100%",
 }}
>
 <input
   type="text"
   value={input}
   onChange={(event) => setInput(event.target.value)}
   style={{
     width: "85%",
     padding: "15px",
     borderRadius: "10px",
     border: "1px solid #bbb",
     backgroundColor: "#e0e0e0",
     color: "#333",
     outline: "none",
     marginLeft: "-19%",
     marginBottom: "1%",
   }}
 />


       <button type="submit" style={{ display: "none" }}>
         send
       </button>
     </form>
   </div>
 );
};


export default Chatbot;
