import axios, { AxiosResponse } from 'axios';

const defaultConfig: any = {
  headers: {
    'Content-Type': 'application/json'
  }
};

export default class API {
  static get(url: string, config: any = {}): Promise<AxiosResponse<any, any>> {
    return axios.get(url, { ...defaultConfig, ...config });
  }

  static post(
    url: string,
    request: any,
    config: any = {}
  ): Promise<AxiosResponse<any, any>> {
    return axios.post(url, request, { ...defaultConfig, ...config });
  }

  static put(
    url: string,
    request: any,
    config: any = {}
  ): Promise<AxiosResponse<any, any>> {
    return axios.put(url, request, { ...defaultConfig, ...config });
  }

  static delete(
    url: string,
    config: any = {}
  ): Promise<AxiosResponse<any, any>> {
    return axios.delete(url, { ...defaultConfig, ...config });
  }
}
