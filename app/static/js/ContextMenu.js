class ContextMenu {
  constructor({ target = null, menuItems = [], mode = "dark" }) {
    this.target = target;
    this.menuItems = menuItems;
    this.mode = mode;
    this.targetNode = this.getTargetNode();
    this.menuItemsNode = this.getMenuItemsNode();
    this.isOpened = false;
    this.clickedElement = null;
  }

  getTargetNode() {
    const nodes = document.querySelectorAll(this.target);

    if (nodes && nodes.length !== 0) {
      return nodes;
    } else {
      console.error(`getTargetNode :: "${this.target}" target not found`);
      return [];
    }
  }

  getMenuItemsNode() {
    const nodes = [];

    if (!this.menuItems) {
      console.error("getMenuItemsNode :: Please enter menu items");
      return [];
    }

    this.menuItems.forEach((data, index) => {
      const item = this.createItemMarkup(data);
      item.firstChild.setAttribute(
        "style",
        `animation-delay: ${index * 0.08}s`
      );
      nodes.push(item);
    });
    return nodes;
  }

  createItemMarkup(data) {
    const button = document.createElement("BUTTON");
    const item = document.createElement("LI");

    button.innerHTML = data.content;
    button.classList.add("contextMenu-button");
    item.classList.add("contextMenu-item");

    if (data.divider) item.setAttribute("data-divider", data.divider);
    item.appendChild(button);

    if (data.events && data.events.length !== 0) {
      Object.entries(data.events).forEach((event) => {

        // give the event the clicked element as a parameter
        const eventHandler = (e) => event[1](e, this.clickedElement);
        button.addEventListener(event[0], eventHandler)
      })
    } else {
      button.addEventListener("click", () => {
        this.closeMenu(item.parentElement);
      });
    }
    return item;
  }

  renderMenu() {
    const menuContainer = document.createElement("UL");

    menuContainer.classList.add("contextMenu");
    menuContainer.setAttribute("data-theme", this.mode);
    
    this.menuItemsNode.forEach((item) => menuContainer.appendChild(item));

    return menuContainer;
  }

  closeMenu(menu) {
    if (this.isOpened) {
      this.isOpened = false;
      menu.remove();
    }
  }

  
  init() {
    const contextMenu = this.renderMenu();
    document.addEventListener("click", () => this.closeMenu(contextMenu));
    window.addEventListener("blur", () => this.closeMenu(contextMenu));
    if (this.targetNode.length === 0) return;
    

    this.targetNode.forEach((target) => {
      
      target.addEventListener("contextmenu", (e) => {
        if (this.isOpened) return;
        e.preventDefault();
        this.isOpened = true;
        this.clickedElement = e.target;
        // log the new element
        const { clientX, clientY } = e;
        document.body.appendChild(contextMenu);

        const positionY =
          clientY + contextMenu.scrollHeight >= window.innerHeight
            ? window.innerHeight - contextMenu.scrollHeight - 20
            : clientY;
        const positionX =
          clientX + contextMenu.scrollWidth >= window.innerWidth
            ? window.innerWidth - contextMenu.scrollWidth - 20
            : clientX;
        contextMenu.setAttribute(
          "style",
          `--width: ${contextMenu.scrollWidth}px;
          --height: ${contextMenu.scrollHeight}px;
          --top: ${positionY}px;
          --left: ${positionX}px;`
        );
      });
    });
  }
}



const deleteIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`;

const addAppIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`;

const toggleThemeIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;

// use a list icon
const toggleViewIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>`;

// use an app refresh icon
const refreshIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3"></path><path d="M21.49 15a9 9 0 0 1-14.85 3"></path></svg>`;

const editIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg>`
// python svg icon
const executePythonCodeIcon = `<svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><title>Python</title><path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z"/></svg>`;
// open icon
const openAppIcon = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M17 8l4 4-4 4M3 12h18"></path></svg>`;

const viewAppLogs = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>`;

// download multiple files icon
const downloadZipIcon = `<svg viewBox="0 0 122.88 120.89" width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="currentColor" style="margin-right: 7px" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><title>download-file</title><path d="M84.58,47a7.71,7.71,0,1,1,10.8,11L66.09,86.88a7.72,7.72,0,0,1-10.82,0L26.4,58.37a7.71,7.71,0,1,1,10.81-11L53.1,63.12l.16-55.47a7.72,7.72,0,0,1,15.43.13l-.15,55L84.58,47ZM0,113.48.1,83.3a7.72,7.72,0,1,1,15.43.14l-.07,22q46,.09,91.91,0l.07-22.12a7.72,7.72,0,1,1,15.44.14l-.1,30h-.09a7.71,7.71,0,0,1-7.64,7.36q-53.73.1-107.38,0A7.7,7.7,0,0,1,0,113.48Z"/></svg>`;

// image plus icon
const changeBackgroundImage = `<svg viewBox="0 0 24 24"  width="13" height="13" stroke="currentColor" stroke-width="2.5" fill="none" style="margin-right: 7px"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 16c1.403-.234 3.637-.293 5.945.243M16 21c-1.704-2.768-4.427-4.148-7.055-4.757m0 0C10.895 13.985 14.558 12 21 12h1M8.5 7C8 7 7 7.3 7 8.5S8 10 8.5 10 10 9.7 10 8.5 9 7 8.5 7z"/><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2m7 0v3m0 3V5m0 0h3m-3 0h-3"/></svg>`;



// after page load
$(document).ready(function() {
  const backgroundMenuItems = [
    { 
      content: `${addAppIcon}Add App`,
      events: {
        // call the id addAppBtn by using jquery
        click: (e) => $("#addAppBtn").click()
       }
    },
    { content: `${toggleThemeIcon}Toggle Theme`,
      events: {
        // call the id toggleDarkModeBtn by using jquery
        click: (e) => $("#toggleDarkModeBtn").click()
        }
    },
    {
      content: `${toggleViewIcon}Toggle App View`,
      events: {
        click: (e) => $("#toggleDisplayModeBtn").click()
      }
    },
    {
      content: `${changeBackgroundImage}Change Background Image`,
      events: {
        click: (e) => $("#changeBackgroundImageBtn").click()
      }
    },
    { 
      content: `${refreshIcon}Refresh Page`,
      divider: "top", // top, bottom, top-bottom
      events: {
        // reload the page
        click: (e) => location.reload()
      }
    }
  ];


  const menuItems = [
    {
      content: `${openAppIcon}Open App`,
      events: {
        click: (e, target) => {
          // get the closest card-link
          const cardLink = $(target).closest(".card-wrapper").find(".card-link").attr("href");
          window.open(cardLink, "_blank");
        }
      }
    },
    { content: `${executePythonCodeIcon}Run App Script`,
      events: {
        click: (e, target) => {
          // get the closest card-link
          const cardLink = $(target).closest(".card-wrapper").find(".card-link").attr("href");
          // get the name of the app
          const appName = cardLink.split("/").pop();
          // api + app name + /run_script {method: POST}
          $.ajax({
            url: `api/app/${appName}/run_script`,
            type: "POST",
            success: function() {
               console.log("Successfully ran script via context menu for app: " + appName);
               alert("Successfully ran script via context menu for app: " + appName);
            },
            error: function() {
              alert("Error running script via context menu for app: " + appName);
            }
          });
        }
      }
    },
    { content: `${downloadZipIcon}Download App Output`,
      events: {
        click: (e, target) => {
          // get the closest card-link
          const cardLink = $(target).closest(".card-wrapper").find(".card-link").attr("href");
          // get the name of the app
          const appName = cardLink.split("/").pop();
          // api + app name + /download_script_output {method: GET}
          $.ajax({
            url: `api/app/${appName}/download_script_output`,
            type: "GET",
            xhrFields: {
              responseType: "blob"
            },
            success: function(data) {
              output = false;
              try {
                if (data.includes("no output")) {
                  output = true;
                }
              } catch (e) {
                output =  false;
              }
              // if "no output" is in the response, then log it as an error
              if (output) {
                console.error("No output to download for app: " + appName);
              } else {
                window.open(`api/app/${appName}/download_script_output`, "_blank");
                console.log("Successfully downloaded output via context menu for app: " + appName);
              }
            },
            error: function() {
              alert("Error downloading output via context menu for app: " + appName);
            }
          });
        }
      }
    },
    { content: `${viewAppLogs}View App Logs`,
      events: {
        click: (e, target) => {
          // get the closest card-link
          const cardLink = $(target).closest(".card-wrapper").find(".card-link").attr("href");
          // get the name of the app
          const appName = cardLink.split("/").pop();
          // api + app name + /get_script_log {method: GET}
          $.ajax({
            url: `api/app/${appName}/get_script_log`,
            type: "GET",
            error: function() {
              alert("Error getting script log via context menu for app: " + appName);
            },
            success: function(data) {
              window.open(`api/app/${appName}/get_script_log`, "_blank");
          }
        });
        }
      }
   },
    {
      content: `${editIcon}Edit App`,
      events: {
        click: (e, target) => {
          const updateButton = $(target).closest(".card-wrapper").find(".app-actions").find(".update-btn");
          updateButton.click();
        }
      }
    },
    { 
      content: `${deleteIcon}Delete App`,
      divider: "top", // top, bottom, top-bottom
      events: {
        // get the name of the app and delete it
        click: (e, target) => {
          const deleteButton = $(target).closest(".card-wrapper").find(".app-actions").find(".delete-btn");
          deleteButton.click();
        }
      }
    }
  ];


  // // wait for .app-card to load
  // const header = new ContextMenu({
  //   target: ".navbar",
  //   menuItems: backgroundMenuItems,
  //   mode: "dark"
  // });
  // set a global theme mode so we can change it from main.js
  window.themeMode = "dark";
  const basicMenu = new ContextMenu({
    // target the header, footer, but not the navbar-start
    target: ".navbar:not(.navbar-start), .footer",
    menuItems: backgroundMenuItems,
    mode: window.themeMode
  });

  const appContextMenu = new ContextMenu({
    target: ".card-wrapper",
    menuItems: menuItems,
    mode: window.themeMode
  });

  //header.init();
  basicMenu.init();
  appContextMenu.init();

});