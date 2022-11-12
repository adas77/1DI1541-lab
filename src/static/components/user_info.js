class UserInfo extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.innerHTML = `
      
      `;//todo
    }
}

customElements.define('user-info', UserInfo);
