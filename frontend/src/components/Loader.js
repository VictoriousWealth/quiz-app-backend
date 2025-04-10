import React from 'react';
import { Spinner } from 'react-bootstrap';

const Loader = () => (
  <div className="text-center my-5">
    <Spinner animation="border" role="status" />
    <div className="mt-2">Generating quiz...</div>
  </div>
);

export default Loader;