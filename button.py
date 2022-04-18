class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, image2=None):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.image2=image2
		self.hovering = False
		self.selected = False
		if self.image2 is not None:
			self.rect2 = self.image2.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			if self.hovering or self.selected:
				screen.blit(self.image2, self.rect2)
			else:
				screen.blit(self.image, self.rect)
		if self.text is not None:	
			screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			if self.image2 is not None:
				self.selected = not self.selected
				print(self.selected)
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

	def changeOutline(self, position):
		if self.image2 is not None and position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.hovering = True
		else:
			self.hovering = False
