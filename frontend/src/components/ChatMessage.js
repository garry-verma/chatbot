import React from 'react';

function ChatMessage({ message }) {
  console.log("message",message.text)
  const renderQueryResults = (results) => {
    if (!Array.isArray(results) || results.length === 0) {
      return <p>No results found.</p>;
    }
  
    return (
      <ul className="list-disc ml-4">
        {results.map((item, index) => {
          if (Array.isArray(item)) {
            // Check if it's a single-element array or a detailed tuple-like array
            if (item.length === 1) {
              return <li key={index}>{item[0]}</li>; // Single-element tuple or array
            } else {
              return (
                <li key={index}>
                  <strong>{item[1]}</strong> - {item[2]} <br />
                  <span>
                    Category: {item[4]}, Price: ${item[3]} <br />
                    Description: <em>{item[5]}</em> <br />
                    Supplier ID: {item[6]}
                  </span>
                </li>
              );
            }
          } else {
            // Assume it's a flat array of strings
            return <li key={index}>{item}</li>;
          }
        })}
      </ul>
    );
  };
  

  

  return (
    <div className={`p-2 ${message.sender === 'user' ? 'bg-gray-200 text-right' : 'bg-blue-200 text-left'}`}>
      <strong>{message.sender === 'user' ? 'You' : 'AI'}:</strong>
      <div className="mt-1">
        {message.sender === 'bot' && (
          <>
            {/* <p className="font-medium">Query Results:</p> */}
            {renderQueryResults(message.text)}
           
            {/* <p className="mt-2 font-medium">Summary:</p>
            <p className="break-words">{message.summary}</p>  */}
          </>
        )}
        {message.sender === 'user' && <p>{message.text}</p>}
      </div>
    </div>
  );
}

export default ChatMessage;
