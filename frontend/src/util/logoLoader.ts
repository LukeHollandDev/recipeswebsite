import HFLogo from "../assets/hello_fresh.png";
import JOCLogo from "../assets/just_one_cookbook.jpg";

const domainToLogo = new Map([
  ["hellofresh.co.uk", HFLogo],
  ["justonecookbook.com", JOCLogo],
]);

// Takes in a URL and if one of the specified domains matches it returns the path to the logo.
export function logoLoader(url: string): string {
  const logoDomains = [...domainToLogo.keys()];
  for (let i = 0; i < logoDomains.length; i++) {
    if (url.toLowerCase().includes(logoDomains[i].toLowerCase())) {
      return domainToLogo.get(logoDomains[i]) ?? "";
    }
  }
  return "";
}
