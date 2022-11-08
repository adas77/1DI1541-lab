class Nav extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
    <style>
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      color: aqua;
      background-color: blueviolet;
    }
    
    .nav {
      margin: auto;
      width: 50%;
      text-align: center;
      border: 3px solid green;
      padding: 10px;
      background-color: #333;
      overflow: hidden;
    }
    
    .nav a {
      float: left;
      color: #f2f2f2;
      text-align: center;
      padding: 14px 16px;
      text-decoration: none;
      font-size: 44px;
    }
    
    .nav a:hover {
      background-color: #ddd;
      color: black;
    }
    
    .nav a.active {
      background-color: #04aa6d;
      color: white;
    }
  </style>

      <div class="nav">
      <ul>
        <li>
          <a href="/api/user/login">Sign in</a>
        </li>
        <li>
          <a href="/api/user/create">Sign Up</a>
        </li>
        <li>
          <a href="/product">Produkty</a>
        </li>
        <li>
          <a href="https://isod.ee.pw.edu.pl/">ISOD</a>
        </li>
        <li>
          <a href="/logout">Logout</a>
        </li>
      </ul>
    </div>
    `;
  }
}

customElements.define('nav-component', Nav);
