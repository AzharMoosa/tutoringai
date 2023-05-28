import * as DOMPurify from 'dompurify';
import 'katex/dist/katex.min.css';
import Latex from 'react-latex-next';

const MessageTextBlock = ({ text }: { text: string }) => (
  <Latex>{DOMPurify.sanitize(text)}</Latex>
);

export default MessageTextBlock;
