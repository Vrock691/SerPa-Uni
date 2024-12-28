# Filter circles based on size and intensity contrast (dark or white with outline)
filtered_circles = []
if circles is not None:
    for circle in circles:
        x, y, r = circle
        # Check intensity of the circle's center and surrounding pixels
        center_intensity = gray[y, x]
        surrounding_intensity = cv2.mean(gray[max(y-r, 0):y+r, max(x-r, 0):x+r])[0]
        intensity_difference = abs(center_intensity - surrounding_intensity)

        # Keep only circles that match the characteristics of large dark or outlined circles
        if r > 20 and (intensity_difference > 30 or center_intensity < 100):
            filtered_circles.append(circle)

    # Ensure we have exactly 4 circles for the transformation
    if len(filtered_circles) == 4:
        # Sort the filtered circles to find approximate corners
        sorted_circles = sorted(filtered_circles, key=lambda c: (c[1], c[0]))

        # Extract the top-left, top-right, bottom-left, bottom-right circles
        top_circles = sorted(sorted_circles[:2], key=lambda c: c[0])  # Top-left, top-right
        bottom_circles = sorted(sorted_circles[2:], key=lambda c: c[0])  # Bottom-left, bottom-right

        rect = np.array([
            [top_circles[0][0], top_circles[0][1]],  # Top-left
            [top_circles[1][0], top_circles[1][1]],  # Top-right
            [bottom_circles[1][0], bottom_circles[1][1]],  # Bottom-right
            [bottom_circles[0][0], bottom_circles[0][1]]   # Bottom-left
        ], dtype='float32')

        # Determine the new image width and height
        width_a = np.linalg.norm(rect[2] - rect[3])  # Bottom width
        width_b = np.linalg.norm(rect[1] - rect[0])  # Top width
        height_a = np.linalg.norm(rect[1] - rect[2])  # Right height
        height_b = np.linalg.norm(rect[0] - rect[3])  # Left height
        max_width = int(max(width_a, width_b))
        max_height = int(max(height_a, height_b))

        # Define the destination points for perspective transform
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype='float32')

        # Perform the perspective transformation
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (max_width, max_height))

        # Display the result
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 2, 1)
        plt.title("Original Image with Filtered Circles")
        for circle in filtered_circles:
            cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            cv2.circle(image, (circle[0], circle[1]), 2, (0, 0, 255), 3)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title("Flattened Image")
        plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
    else:
        print("Could not find exactly 4 circles for transformation. Found:", len(filtered_circles))
else:
    print("No circles detected in the image.")
