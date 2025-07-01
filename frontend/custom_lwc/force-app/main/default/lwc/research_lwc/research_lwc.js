import { LightningElement, track } from 'lwc';
import fetchTicker from '@salesforce/apex/ResearchController.fetchTicker';

export default class Research_lwc extends LightningElement {
  @track searchTerm = '';
  @track result = null;

  handleInputChange(event) {
    this.searchTerm = event.target.value;
  }

  async handleSearch() {

    const raw = await fetchTicker({ ticker: this.searchTerm });
    const json = JSON.parse(raw);
    const data = json.message;

    this.result = {
      name: data.longName,
      price: data.currentPrice ?? 'N/A',
      sector: data.sector,
      pe: data.forwardPE
    };

  }
}
