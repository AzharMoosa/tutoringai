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
    <div
      style={{ marginLeft: `${info.flipped ? '4rem' : '0rem'}` }}
      className="service-info-content"
    >
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

  const ServiceInfoImage = <div className="service-info-image"></div>;

  return (
    <div className={`service-info ${border && 'service-info-border'}`}>
      {info.flipped ? ServiceInfoImage : ServiceInfoContent}
      {info.flipped ? ServiceInfoContent : ServiceInfoImage}
    </div>
  );
};

export default ServiceInfo;
