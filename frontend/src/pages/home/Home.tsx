import React from 'react';
import FeatureBox from '../../components/home/FeatureBox';
import Footer from '../../components/home/Footer';
import InfoBox from '../../components/home/InfoBox';
import Navbar from '../../components/home/Navbar';
import ServiceInfo from '../../components/home/ServiceInfo';
import Button from '../../components/util/Button';
import Title from '../../components/util/Title';
import './Home.css';

const Home = () => {
  return (
    <div className="landing-page">
      <div className="silver-bg">
        <div className="container">
          <div className="navbar">
            <Title />
            <Navbar />
            <Button textContent="Login" small={true} />
          </div>
          <div id="home">
            <h1>Lorem Ipsum Dolor Sit Amet Consect Adipiscing Elit.</h1>
            <h3>
              consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus
              aliquet a libero ut cursus. Mauris
            </h3>
            <div className="button-layout">
              <Button textContent="Get Started" icon="faArrowRight" />
              <Button
                textContent="Learn More"
                icon="faArrowRight"
                primary={false}
              />
            </div>
          </div>
          <div id="about">
            <InfoBox
              title="Box 1"
              icon=""
              textContent="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus."
            />
            <InfoBox
              title="Box 2"
              icon=""
              textContent="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus."
            />
            <InfoBox
              title="Box 3"
              icon=""
              textContent="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus."
            />
          </div>
        </div>
      </div>
      <div className="container">
        <div id="features">
          <h1>M.A.R.C</h1>
          <div className="features-grid">
            <FeatureBox
              title={'Title 1'}
              textContent={
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus. Aliquam non ultricies risus, ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu. Pellentesque ac eros ultricies, ornare elit vel, rutrum mi. Nunc risus eros, fringilla et consequat in, varius vel leo. Interdum et malesuada'
              }
            />
            <FeatureBox
              title={'Title 2'}
              textContent={
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus. Aliquam non ultricies risus, ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu. Pellentesque ac eros ultricies, ornare elit vel, rutrum mi. Nunc risus eros, fringilla et consequat in, varius vel leo. Interdum et malesuada'
              }
            />
            <FeatureBox
              title={'Title 3'}
              textContent={
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus. Aliquam non ultricies risus, ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu. Pellentesque ac eros ultricies, ornare elit vel, rutrum mi. Nunc risus eros, fringilla et consequat in, varius vel leo. Interdum et malesuada'
              }
            />
            <FeatureBox
              title={'Title 4'}
              textContent={
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris ullamcorper posuere ex non ultricies. Aliquam congue mi finibus pharetra finibus. Aliquam non ultricies risus, ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu. Pellentesque ac eros ultricies, ornare elit vel, rutrum mi. Nunc risus eros, fringilla et consequat in, varius vel leo. Interdum et malesuada'
              }
            />
          </div>
        </div>

        <div id="services">
          <ServiceInfo
            title="Heading One"
            subHeading={
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel '
            }
            description={
              'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.'
            }
            boxOne={{
              title: 'Heading',
              description:
                'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.',
              icon: ''
            }}
            boxTwo={{
              title: 'Heading',
              description:
                'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.',
              icon: ''
            }}
          />
          <ServiceInfo
            title="Heading One"
            subHeading={
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel '
            }
            description={
              'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.'
            }
            boxOne={{
              title: 'Heading',
              description:
                'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.',
              icon: ''
            }}
            boxTwo={{
              title: 'Heading',
              description:
                'Aliquam congue mi finibus pharetra finibus. Ultricies risus ac consectetur metus. Ut quis augue eu velit sagittis fermentum nec a arcu.',
              icon: ''
            }}
            flipped={true}
          />
        </div>

        <div id="contact">
          <Footer />
        </div>
      </div>
    </div>
  );
};

export default Home;
