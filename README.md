# robscotton.com

The picture-book website of Rob Scotton: Splat the Cat, Russell the Sheep and Max and Moonbean.

- `site/` is the live website. Render publishes this folder as it is; there is no build step.
- `tools/` holds the scripts that generated it (`build.py` writes the pages, `make_images.py` cuts the display-size images, `make_activities.py` makes the Max printables, `make_dist.py` assembles this repository). They need Rob's original artwork, which is not stored here.
- `render.yaml` tells Render how to serve the site.

Artwork © Rob Scotton. All rights reserved. The images in this repository are display copies only and may not be reused.
