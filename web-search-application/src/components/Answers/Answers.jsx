import React from "react";
import App from "../../App";

import { Card, CardContent, Typography, Grid } from "@material-ui/core";

import styles from "./Answers.module.css";

import values from "../../values.json";

import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

const Answers = (props) => {
  var rows = [];
  if (props.display) {
    rows.push(
      <Grid item xs={12} md={10} className={styles.gap}>
        <Card className={styles.specialcard}>
          <CardContent>
            <Accordion defaultExpanded>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
              >
                <Typography variant="h5" component="h2">
                  1) Question: {values.question}
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <br></br>
                <br></br>
                <Typography variant="body2" component="p">
                  Answer: {values.answer}
                </Typography>
              </AccordionDetails>
            </Accordion>
          </CardContent>
        </Card>
      </Grid>
    );
    for (var i = 2; i < 11; i++) {
      rows.push(
        <Grid item xs={12} md={10} className={styles.gap}>
          <Card className={styles.card}>
            <CardContent>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel1a-content"
                  id="panel1a-header"
                >
                  <Typography variant="h5" component="h2">
                    {i}) Question: {values.question}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <br></br>
                  <br></br>
                  <Typography variant="body2" component="p">
                    Answer: {values.answer}
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </CardContent>
          </Card>
        </Grid>
      );
    }
  }
  return (
    <div>
      <Grid container>{rows}</Grid>
    </div>
  );
};
export default Answers;
