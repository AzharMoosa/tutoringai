import TopicBox from '../../components/home/TopicBox';
import Footer from '../../components/home/Footer';
import InfoBox from '../../components/home/InfoBox';
import Navbar from '../../components/home/Navbar';
import ServiceInfo from '../../components/home/ServiceInfo';
import Button from '../../components/util/Button';
import Title from '../../components/util/Title';
import './Home.css';
import { Link } from 'react-router-dom';
import {
  aboutBoxInfo,
  AboutInfo,
  serviceBoxInfo,
  topicBoxInfo,
  TopicInfo
} from '../../data/landingPageConstants';
import heroImg from '../../assets/images/hero-image.png';

const Home = () => {
  return (
    <div className="landing-page">
      <div className="bg-cover">
        <div className="container">
          <div className="navbar">
            <Title />
            <Navbar />
            <Link className="login-btn" to="/login">
              <h4>Login</h4>
            </Link>
          </div>
          <div id="home">
            <div className="home-left">
              <h1>M.A.R.C</h1>
              <h3>
                An intelligent tutoring chatbot to help you revise mathematics
                and assess your understanding.
              </h3>
              <div className="button-layout">
                <Link to="/login">
                  <Button textContent="Get Started" />
                </Link>
              </div>
            </div>

            <div className="home-right">
              <img src={heroImg} alt="hero-img" />
            </div>
          </div>
        </div>
      </div>

      <div className="container">
        <div id="about">
          <h1>Who is M.A.R.C?</h1>
          <div className="about-grid">
            {aboutBoxInfo.map((info: AboutInfo, index) => (
              <InfoBox key={index} info={info}></InfoBox>
            ))}
          </div>
        </div>
      </div>

      <div id="topics">
        <div className="container">
          <h1>Topics</h1>
          <div className="topics-grid">
            {topicBoxInfo.map((info: TopicInfo, index) => (
              <TopicBox info={info} key={index} />
            ))}
          </div>
        </div>
      </div>
      <div className="container">
        <div id="services">
          {serviceBoxInfo.map((info, idx) => (
            <ServiceInfo
              key={idx}
              info={info}
              border={idx !== serviceBoxInfo.length - 1}
            />
          ))}
        </div>
      </div>

      <div id="contact">
        <Footer />
      </div>
    </div>
  );
};

export default Home;
