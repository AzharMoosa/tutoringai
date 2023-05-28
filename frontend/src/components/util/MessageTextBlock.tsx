import * as DOMPurify from 'dompurify';
import 'katex/dist/katex.min.css';
import Latex from 'react-latex-next';

const MessageTextBlock = ({ text }: { text: string }) => {
  return text !== '' ? (
    <Latex>{DOMPurify.sanitize(text)}</Latex>
  ) : (
    <div className="blinking-pointer"></div>
  );
};
export default MessageTextBlock;
