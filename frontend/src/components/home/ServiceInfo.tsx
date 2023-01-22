import React from 'react';
import './ServiceInfo.css';
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

const ServiceInfo = ({
  title,
  subHeading,
  description,
  boxOne,
  boxTwo,
  flipped = false
}: ServiceInfoStyle) => {
  const ServiceInfoContent = (
    <div
      style={{ marginLeft: `${flipped ? '4rem' : '0rem'}` }}
      className="service-info-content"
    >
      <h2>{title}</h2>
      <h3>{subHeading}</h3>
      <p>{description}</p>
      <div className="service-info-box">
        <div className="service-info-box-img"></div>
        <div className="service-info-box-txt">
          <h4>{boxOne.title}</h4>
          <p>{boxOne.description}</p>
        </div>
      </div>
      <div className="service-info-box">
        <div className="service-info-box-img"></div>
        <div className="service-info-box-txt">
          <h4>{boxTwo.title}</h4>
          <p>{boxTwo.description}</p>
        </div>
      </div>
    </div>
  );

  const ServiceInfoImage = <div className="service-info-image"></div>;

  return (
    <div className="service-info">
      {flipped ? ServiceInfoImage : ServiceInfoContent}
      {flipped ? ServiceInfoContent : ServiceInfoImage}
    </div>
  );
};

export default ServiceInfo;
