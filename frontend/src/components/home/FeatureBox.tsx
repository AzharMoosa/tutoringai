import React from 'react';
import './FeatureBox.css';

interface FeatureBoxStyle {
  title: string;
  textContent: string;
}

const FeatureBox = ({ title, textContent }: FeatureBoxStyle) => {
  return (
    <div className="feature-box">
      <h2>{title}</h2>
      <p>{textContent}</p>
    </div>
  );
};

export default FeatureBox;
