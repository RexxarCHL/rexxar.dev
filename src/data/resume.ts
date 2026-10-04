import yaml from 'js-yaml';
import raw from './resume.yaml?raw';

export interface Resume {
  experience: {
    org: string;
    location: string;
    role: string;
    start: string;
    end: string;
    highlights: string[];
  }[];
  education: { school: string; degree: string; end: string }[];
  patents: { title: string; number: string; date: string; note: string }[];
  skills: Record<string, string[]>;
}

export const resume = yaml.load(raw) as Resume;

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "2019-11" -> "Nov 2019"; anything else is returned as-is. */
export function formatMonth(value: string): string {
  const m = /^(\d{4})-(\d{2})$/.exec(String(value));
  return m ? `${MONTHS[Number(m[2]) - 1]} ${m[1]}` : String(value);
}
