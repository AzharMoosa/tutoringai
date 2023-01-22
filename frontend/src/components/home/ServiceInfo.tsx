import React from 'react';

export interface ServiceBox {
  title: string;
  description: string;
  icon: string;
}

interface ServiceInfoStyle {
  title: string;
  subHeading: string;
  description: string;
  boxOne: ServiceBox;
  boxTwo: ServiceBox;
  flipped?: boolean;
}

const ServiceInfo = ({ flipped = false }: ServiceInfoStyle) => {
  return <div>ServiceInfo</div>;
};

export default ServiceInfo;
