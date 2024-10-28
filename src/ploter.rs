// use plotters::prelude::*;
pub mod ploter{
    use plotters::prelude::*;
    pub fn example() -> Result<(), Box<dyn std::error::Error>> {
        let root_drawing_area =
            BitMapBackend::new("test/4.png", (3000, 2000)).into_drawing_area();
        // And we can split the drawing area into 3x3 grid
        let child_drawing_areas = root_drawing_area.split_evenly((3000, 3000));
        // Then we fill the drawing area with different color
        for (area, color) in child_drawing_areas.into_iter().zip(0..) {
            area.fill(&Palette99::pick(color))?;
        }
        root_drawing_area.present()?;
        Ok(())
    }
}
