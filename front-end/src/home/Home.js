import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Container, Paper, Grid, Typography } from "@material-ui/core";
import InfoOutlinedIcon from "@material-ui/icons/InfoOutlined";

export class Home extends Component {
  static propTypes = {};

  render() {
    return (
      <div className="my-30">
        <Typography variant="h6" gutterBottom>
          Vulnerability Management Overview
        </Typography>
        <div className="mt-20">
          <Grid container spacing={3}>
            <Grid item xs={8}>
              <Typography variant="subtitle1" gutterBottom>
                <span>Statistics </span>
                <InfoOutlinedIcon fontSize="inherit" />
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={4}>
                  <Paper className="p-20">
                    <Grid container spacing={3}>
                      <Grid item xs={6}>
                        <Typography variant="caption" display="block">
                          VULNERABILITIES
                        </Typography>

                        <Typography variant="h2" display="inline">
                          2.2
                        </Typography>
                        <Typography variant="h6" display="inline">
                          K
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" display="block">
                          SEVERITY
                        </Typography>
                        <Typography variant="h6" display="inline">
                          <span>4 </span>
                        </Typography>
                        <Typography
                          variant="caption"
                          display="inline"
                          className="ml-5"
                        >
                          Critical
                        </Typography>
                        <br />
                        <Typography variant="h6" display="inline">
                          <span>608 </span>
                        </Typography>
                        <Typography
                          variant="caption"
                          display="inline"
                          className="ml-5"
                        >
                          High
                        </Typography>
                      </Grid>
                    </Grid>
                  </Paper>
                </Grid>
                <Grid item xs={4}>
                  Test
                </Grid>
                <Grid item xs={4}>
                  Test
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="subtitle1" gutterBottom>
                <span>Scan Coverage </span>
                <InfoOutlinedIcon fontSize="inherit" />
              </Typography>
            </Grid>
          </Grid>
        </div>
      </div>
    );
  }
}

export default Home;
