import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
} from "streamlit-component-lib";
import React, { useEffect, useRef, useState } from "react";

function Graph({ args, disabled, theme }: ComponentProps) {
  const { elem } = args;

  const graphContainerRef = useRef<HTMLDivElement>(null);
  const [selection, setSelection] = useState("");

  const initializeGraph = () => {
    if (graphContainerRef.current) {
      graphContainerRef.current.innerHTML = elem; // Inject original HTML first

      // Execute drawGraph script
      const scripts = graphContainerRef.current.getElementsByTagName("script");
      let drawGraphScriptFound = false;
      for (let i = 0; i < scripts.length; i++) {
        if (scripts[i].innerHTML.includes("drawGraph")) {
          const newScript = document.createElement("script");
          newScript.text = scripts[i].innerHTML;
          document.body.appendChild(newScript);
          drawGraphScriptFound = true;
          break;
        }
      }

      // Add click handler after drawGraph
      const clickScript = document.createElement("script");
      clickScript.text = `
        if (typeof network !== "undefined") {
          network.on("click", function (params) {
            if (params.nodes.length > 0) {
              window.postMessage({ type: "nodeSelected", node: params.nodes[0] }, "*");
            } 
          });
        }
      `;
      document.body.appendChild(clickScript);
    }
  };

  useEffect(() => {
    if (typeof window.vis === "undefined") {
      const script = document.createElement("script");
      script.src =
        "https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js";
      script.integrity =
        "sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==";
      script.crossOrigin = "anonymous";
      script.onload = () => {
        initializeGraph();
      };
      document.body.appendChild(script);
    } else {
      initializeGraph();
    }

    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === "nodeSelected" && event.data.node) {
        setSelection(event.data.node);
      }
    };
    window.addEventListener("message", handleMessage);

    Streamlit.setFrameHeight();

    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, [elem]); // Dependency on elem

  useEffect(() => {
    Streamlit.setComponentValue(selection);
  }, [selection]);

  return (
    <div
      ref={graphContainerRef}
      style={{
        width: "104%",
        height: "600px",
        marginTop: "-10px",
        marginLeft: "-5px",
        margin: "-10px ",
        overflow: "hidden",
      }}
    />
  );
}

export default withStreamlitConnection(Graph);