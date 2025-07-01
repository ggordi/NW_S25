import { LightningElement, track } from 'lwc';

export default class Research_lwc extends LightningElement {
  @track searchTerm = '';
  @track result = null;

  handleInputChange(event) {
    this.searchTerm = event.target.value;
  }

  async handleSearch() {
    console.log('Search button clicked');
    console.log('Search term:', this.searchTerm);

    const resp = await fetch(`https://nw-s25.onrender.com/research/${this.searchTerm}`);
    const json = await resp.json();
    const data = json.message;

    // Placeholder: set dummy result for now
    this.result = {
      name: data.longName,
      price: data.price,
      sector: data.sector,
      pe: data.forwardPE
    };
  }
}
