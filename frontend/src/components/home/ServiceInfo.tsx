import { ServiceDetails } from '../../data/landingPageConstants';
import './ServiceInfo.css';

const ServiceInfo = ({
  info,
  border
}: {
  info: ServiceDetails;
  border: boolean;
}) => {
  const ServiceInfoContent = (
    <div className="service-info-content">
      <h2>{info.title}</h2>
      <p>{info.description}</p>
      <div className="service-info-boxes">
        <div className="service-info-box">
          <h4>{info.boxOne.title}</h4>
          <p>{info.boxOne.description}</p>
        </div>
        <div className="service-info-box">
          <h4>{info.boxTwo.title}</h4>
          <p>{info.boxTwo.description}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className={`service-info ${border && 'service-info-border'}`}>
      {ServiceInfoContent}
    </div>
  );
};

export default ServiceInfo;
