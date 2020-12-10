import React from "react";

import { Search, Answers } from "./components";
import styles from "./App.module.css";
import { createMuiTheme, withStyles, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { green } from '@material-ui/core/colors';

const BootstrapButton = withStyles({
  root: {
    boxShadow: 'none',
    textTransform: 'none',
    align:'center',
    fontSize: 16,
    marginLeft: '680px',
    padding: '6px 12px',
    border: '1px solid',
    lineHeight: 1.5,
    backgroundColor: 'green',
    borderColor: '#0063cc',
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    '&:hover': {
      backgroundColor: '#0069d9',
      borderColor: '#0062cc',
      boxShadow: 'none',
    },
    '&:active': {
      boxShadow: 'none',
      backgroundColor: '#0062cc',
      borderColor: '#005cbf',
    },
    '&:focus': {
      boxShadow: '0 0 0 0.2rem rgba(0,123,255,.5)',
    },
  },
})(Button);


class App extends React.Component {
  state = {
    display: false,
  };
  displayCards= () => {
    this.setState ({
      display: !this.state.display
    })
  }

  render() {
    return (
      <div className={styles.container}>
        <Search />
        <BootstrapButton variant="contained" color="primary" disableRipple onClick = {this.displayCards}>
          Search
        </BootstrapButton>
        <br></br>
        <br></br>
        <Answers display={this.state.display} />
      </div>
    );
  }
}

export default App;
