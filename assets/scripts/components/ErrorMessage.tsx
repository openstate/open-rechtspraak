import React from 'react';

function ErrorMessage() {
  return (
    <p className="text-danger">
      Er is een onbekende fout opgetreden. Probeer het later opnieuw of neem
      {' '}
      <a href="https://openstate.eu/nl/contact/">direct contact</a>
      {' '}
      met ons op.
    </p>
  );
}

export default ErrorMessage;
