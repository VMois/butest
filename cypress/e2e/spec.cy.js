const STORE_MAIN_PAGE = 'https://butopea.com'

describe('Butest', () => {
  it('right square contains image', () => {
    cy.visit(STORE_MAIN_PAGE)
    cy.get('.banner-square-column')
        .eq(2)
        .find('img')
        .should('be.visible')
        .should('has.attr', 'src')
        .then((src) => {
          cy.log(src)
        })
  })

  it('square contains text', () => {
    cy.visit(STORE_MAIN_PAGE)
    cy.get('.banner-square-overlay p')
        .should('contain.text', 'Egy pince lakás lenyűgöző felújítása')
        .then((el) => {
          cy.log(el.text())
        })

    cy.get('.banner-square-overlay button')
        .should('contain.text', 'Megnézem!')
        .then((el) => {
          cy.log(el.text())
        })
  })

  it('product list', () => {
    cy.visit(STORE_MAIN_PAGE)
    cy.get('nav button').eq(2).click()

    cy.get('div.product-listing')
        .should('be.visible')
        .should('not.be.empty')

    cy.get('div.product-listing > div > div.product')
        .each(($el, index, $list) => {
          cy.wrap($el).find('a')
              .should('has.attr', 'href')
              .then(href => cy.log(`Link to product: ${href}`))

          cy.wrap($el).find('img')
              .eq(1)
              .should('has.attr', 'src')
              .then(src => cy.log(`Image link of product: ${src}`))

          cy.wrap($el).find('p.product-name')
              .eq(0)
              .then(el => cy.log(`Title of product: ${el.text()}`))

          // TODO: probably type in the code below; not "tile" but "title"
          cy.wrap($el).find('div.product-tile-info > div')
              .eq(0)
              .then(el => cy.log(`Price of product: ${el.text()}`))
        })
  })
})