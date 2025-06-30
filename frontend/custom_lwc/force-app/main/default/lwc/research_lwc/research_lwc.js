import { LightningElement, track } from 'lwc';

export default class Research_lwc extends LightningElement {
  @track searchTerm = '';
  @track result = null;

  handleInputChange(event) {
    this.searchTerm = event.target.value;
  }

  handleSearch() {
    console.log('Search button clicked');
    console.log('Search term:', this.searchTerm);

    // Placeholder: set dummy result for now
    this.result = {
      name: 'Example Corp',
      price: '123.45',
      sector: 'Technology'
    };
  }
}
