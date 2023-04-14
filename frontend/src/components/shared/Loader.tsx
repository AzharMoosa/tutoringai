import React from 'react';
import { Oval, ThreeDots } from 'react-loader-spinner';

const OvalLoader = () => (
  <Oval
    height={80}
    width={80}
    color="#4fa94d"
    wrapperStyle={{}}
    wrapperClass=""
    visible={true}
    ariaLabel="oval-loading"
    secondaryColor="#4fa94d"
    strokeWidth={3}
    strokeWidthSecondary={2}
  />
);

const DotLoader = () => (
  <ThreeDots
    height="80"
    width="80"
    radius="9"
    color="#4fa94d"
    ariaLabel="three-dots-loading"
    wrapperStyle={{}}
    wrapperClass=""
    visible={true}
  />
);

interface ILoaderType {
  loaderType: LoaderType;
}

export enum LoaderType {
  Oval,
  Dots
}

const loaderSelector = (loaderType: LoaderType) => {
  switch (loaderType) {
    case LoaderType.Oval:
      return <OvalLoader />;
    case LoaderType.Dots:
      return <DotLoader />;
    default:
      return <OvalLoader />;
  }
};

const Loader = ({ loaderType }: ILoaderType) => (
  <div className="loader">{loaderSelector(loaderType)}</div>
);

export default Loader;
