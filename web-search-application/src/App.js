import React from "react";

import { Search, Answers } from "./components";
import styles from "./App.module.css";

class App extends React.Component {
  render() {
    return (
      <div className={styles.container}>
        <Search />
        <Answers />
      </div>
    );
  }
}

export default App;
